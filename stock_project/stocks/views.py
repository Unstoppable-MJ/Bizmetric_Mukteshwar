from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yfinance as yf

from .models import Stock, PortfolioStock
from portfolio.models import Portfolio
from .serializers import AddStockSerializer, StockListSerializer

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta


# -----------------------------
# 🔐 LOGIN API
# -----------------------------
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            return Response({
                "message": "Login successful",
                "username": user.username
            })
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )


# -----------------------------
# 📂 PORTFOLIO LIST API
# -----------------------------
class PortfolioListAPIView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        data = [{"id": p.id, "name": p.name, "description": p.description} for p in portfolios]
        return Response(data)

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description", "")
        
        if not name:
            return Response({"error": "Portfolio name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # For now, just link to the first user or create one since there's no auth
        from django.contrib.auth.models import User
        user = User.objects.first()
        if not user:
            user = User.objects.create(username="testuser")

        portfolio = Portfolio.objects.create(name=name, description=description, user=user)

        return Response({
            "message": "Portfolio created successfully",
            "portfolio": {"id": portfolio.id, "name": portfolio.name, "description": portfolio.description}
        }, status=status.HTTP_201_CREATED)

    def patch(self, request):
        portfolio_id = request.data.get("id")
        if not portfolio_id:
            return Response({"error": "Portfolio id required"}, status=400)
            
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            if "name" in request.data:
                portfolio.name = request.data["name"]
            if "description" in request.data:
                portfolio.description = request.data["description"]
            portfolio.save()
            return Response({"message": "Portfolio updated successfully"})
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=404)

    def delete(self, request):
        portfolio_id = request.GET.get("id")
        if not portfolio_id:
            return Response({"error": "Portfolio id required"}, status=400)
            
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            portfolio.delete()
            return Response({"message": "Portfolio deleted successfully"})
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=404)


# -----------------------------
# ➕ ADD STOCK API
# -----------------------------
class AddStockAPIView(APIView):

    def post(self, request):
        serializer = AddStockSerializer(data=request.data)

        if serializer.is_valid():

            symbol = serializer.validated_data['symbol'].upper()
            quantity = serializer.validated_data['quantity']
            portfolio = serializer.validated_data['portfolio']

            yahoo_symbol = symbol + ".NS"

            try:
                ticker = yf.Ticker(yahoo_symbol)
                data = ticker.info

                current_price = data.get("currentPrice")
                pe_ratio = data.get("trailingPE")
                company_name = data.get("shortName", symbol)
                sector = data.get("sector", "Unknown")
                max_price = data.get("fiftyTwoWeekHigh", 0)

                if current_price is None:
                    return Response(
                        {"error": "Invalid stock symbol"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Basic fair value logic
                fair_price = current_price * 1.1
                discount_level = ((fair_price - current_price) / fair_price) * 100
                opportunity = discount_level if discount_level > 0 else 0

                stock_obj, created = Stock.objects.get_or_create(
                    symbol=yahoo_symbol,
                    defaults={
                        "name": company_name,
                        "sector": sector
                    }
                )

                portfolio_stock = PortfolioStock.objects.filter(portfolio=portfolio, stock=stock_obj).first()
                if portfolio_stock:
                    # Aggregate existing stock
                    old_qty = float(portfolio_stock.quantity)
                    old_buy_price = float(portfolio_stock.buy_price)
                    new_qty = float(quantity)
                    new_buy_price = float(current_price)
                    
                    total_qty = old_qty + new_qty
                    avg_buy_price = ((old_qty * old_buy_price) + (new_qty * new_buy_price)) / total_qty if total_qty > 0 else 0
                    
                    portfolio_stock.quantity = total_qty
                    portfolio_stock.buy_price = avg_buy_price
                    portfolio_stock.current_price = current_price
                    portfolio_stock.pe_ratio = pe_ratio if pe_ratio else 0
                    portfolio_stock.max_price = max_price
                    portfolio_stock.discount_level = discount_level
                    portfolio_stock.opportunity = opportunity
                    portfolio_stock.save()
                else:
                    # Create new stock entry
                    PortfolioStock.objects.create(
                        portfolio=portfolio,
                        stock=stock_obj,
                        quantity=quantity,
                        buy_price=current_price,
                        current_price=current_price,
                        pe_ratio=pe_ratio if pe_ratio else 0,
                        max_price=max_price,
                        discount_level=discount_level,
                        opportunity=opportunity
                    )

                return Response({"message": "Stock added successfully"})

            except Exception as e:
                return Response({"error": str(e)}, status=400)

        return Response(serializer.errors, status=400)


# -----------------------------
# 📊 STOCK LIST API
# -----------------------------
class StockListAPIView(APIView):
    def get(self, request):
        portfolio_id = request.GET.get("portfolio_id")
        
        if portfolio_id and portfolio_id != "all":
            stocks = PortfolioStock.objects.filter(portfolio_id=portfolio_id)
        else:
            stocks = PortfolioStock.objects.all()

        serializer = StockListSerializer(stocks, many=True)
        return Response(serializer.data)


# -----------------------------
# 🔎 STOCK PREVIEW API
# -----------------------------
class StockPreviewAPIView(APIView):
    def get(self, request):
        symbol = request.GET.get("symbol")

        if not symbol:
            return Response({"error": "Symbol required"}, status=400)

        yahoo_symbol = symbol.upper() + ".NS"

        try:
            ticker = yf.Ticker(yahoo_symbol)
            data = ticker.info

            current_price = data.get("currentPrice")
            pe_ratio = data.get("trailingPE")
            company_name = data.get("shortName", symbol)
            max_price = data.get("fiftyTwoWeekHigh", 0)
            sector = data.get("sector", "Unknown")

            if current_price is None:
                return Response({"error": "Invalid symbol"}, status=400)

            fair_price = current_price * 1.1
            discount_level = ((fair_price - current_price) / fair_price) * 100
            opportunity = discount_level if discount_level > 0 else 0

            # Fetch 1 month historical data for the chart
            hist_data = ticker.history(period="1mo")
            history_list = []
            
            if not hist_data.empty:
                for date, row in hist_data.iterrows():
                    history_list.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "close": round(row['Close'], 2)
                    })

            return Response({
                "symbol": yahoo_symbol,
                "company_name": company_name,
                "current_price": current_price,
                "max_price": max_price,
                "sector": sector,
                "pe_ratio": pe_ratio,
                "discount_level": discount_level,
                "opportunity": opportunity,
                "history": history_list
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# -----------------------------
# 📈 PORTFOLIO GROWTH API
# -----------------------------
class PortfolioGrowthAPIView(APIView):
    def get(self, request):
        portfolio_id = request.GET.get("portfolio_id")
        if not portfolio_id:
            return Response({"error": "portfolio_id required"}, status=400)

        # Get all stocks in the portfolio
        stocks = PortfolioStock.objects.filter(portfolio_id=portfolio_id).select_related('stock')
        if not stocks:
            return Response([])

        # Aggregate how many total shares we have of each symbol and the weighted avg buy price
        # (This is already handled by our dedup logic, but good practice to iterate the exact holdings)
        holdings = []
        symbols = []
        for s in stocks:
            sym = s.stock.symbol
            qty = float(s.quantity)
            buy_price = float(s.buy_price)
            holdings.append({'symbol': sym, 'qty': qty, 'buy_price': buy_price})
            if sym not in symbols:
                symbols.append(sym)

        try:
            # Download 1 month of historical close prices for all unique symbols
            import pandas as pd
            data = yf.download(symbols, period="1mo", interval="1d", group_by='ticker', progress=False)

            # Reformat downloaded data into a daily lookup map
            # day_map[date_string] = { "TCS.NS": 3500, "INFY.NS": 1400 }
            day_map = {}
            dates_ordered = []

            if len(symbols) == 1:
                symbol = symbols[0]
                for date, row in data.dropna().iterrows():
                    d_str = date.strftime("%Y-%m-%d")
                    if d_str not in day_map:
                        day_map[d_str] = {}
                        dates_ordered.append(d_str)
                    day_map[d_str][symbol] = float(row['Close'])
            else:
                for symbol in symbols:
                    try:
                        ticker_df = data[symbol].dropna()
                        for date, row in ticker_df.iterrows():
                            d_str = date.strftime("%Y-%m-%d")
                            if d_str not in day_map:
                                day_map[d_str] = {}
                                if d_str not in dates_ordered:
                                    dates_ordered.append(d_str)
                            day_map[d_str][symbol] = float(row['Close'])
                    except Exception as e:
                        print(f"Failed extracting {symbol}: {e}")

            # Ensure dates are sorted chronologically
            dates_ordered.sort()

            growth_data = []

            for date_str in dates_ordered:
                day_prices = day_map[date_str]
                total_invested = 0
                total_current = 0

                for h in holdings:
                    sym = h['symbol']
                    qty = h['qty']
                    buy = h['buy_price']
                    
                    # If we have a price for this stock on this day, use it.
                    # Otherwise, use the buy_price as a fallback (assuming no data means market closed/delisted)
                    current = day_prices.get(sym, buy)
                    
                    total_invested += float(buy * qty)
                    total_current += float(current * qty)

                growth_data.append({
                    "date": date_str,
                    "Investment": round(total_invested, 2),
                    "Current": round(total_current, 2)
                })

            return Response(growth_data)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# -----------------------------
# 📈 MULTI-STOCK HISTORY API
# -----------------------------
class MultiStockHistoryAPIView(APIView):
    def get(self, request):
        portfolio_id = request.GET.get("portfolio_id")
        if not portfolio_id:
            return Response({"error": "portfolio_id required"}, status=400)

        stocks = PortfolioStock.objects.filter(portfolio_id=portfolio_id).select_related('stock')
        symbols = [s.stock.symbol for s in stocks]

        if not symbols:
            return Response({})

        try:
            # Download multiple symbols at once
            import pandas as pd
            data = yf.download(symbols, period="1mo", interval="1d", group_by='ticker', progress=False)
            
            result = {}
            # Handle single symbol case vs multiple symbols case in yf.download result structure
            if len(symbols) == 1:
                symbol = symbols[0]
                symbol_data = []
                for date, row in data.dropna().iterrows():
                    symbol_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "close": round(row['Close'], 2)
                    })
                result[symbol] = symbol_data
            else:
                for symbol in symbols:
                    symbol_data = []
                    # Check if symbol column exists (yf.download can be tricky with multi-index)
                    try:
                        ticker_df = data[symbol].dropna()
                        for date, row in ticker_df.iterrows():
                            symbol_data.append({
                                "date": date.strftime("%Y-%m-%d"),
                                "close": round(row['Close'], 2)
                            })
                    except:
                        pass
                    result[symbol] = symbol_data

            return Response(result)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# -----------------------------
# 🗑️ PORTFOLIO STOCK DETAIL API
# -----------------------------
class PortfolioStockDetailAPIView(APIView):
    def delete(self, request, pk):
        try:
            stock_entry = PortfolioStock.objects.get(pk=pk)
            stock_entry.delete()
            return Response({"message": "Asset removed from portfolio"})
        except PortfolioStock.DoesNotExist:
            return Response({"error": "Asset not found"}, status=404)


# -----------------------------
# 🔮 STOCK PREDICTION API (Linear Regression)
# -----------------------------
class StockPredictionAPIView(APIView):
    def get(self, request):
        import numpy as np
        from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
        symbol = request.GET.get("symbol")
        horizon_param = request.GET.get("horizon", "7d")
        algorithm = request.GET.get("algorithm", "linear").lower()

        if not symbol:
            return Response({"error": "Symbol required"}, status=400)

        yahoo_symbol = symbol.upper() if symbol.endswith(".NS") else symbol.upper() + ".NS"

        # Map UI Horizon choice to prediction length and historical training baseline
        horizon_map = {
            "7d": (7, "6mo"),
            "1mo": (30, "1y"),
            "6mo": (180, "2y"),
            "1y": (365, "5y")
        }
        days_to_predict, history_period = horizon_map.get(horizon_param, (7, "6mo"))

        try:
            ticker = yf.Ticker(yahoo_symbol)
            df = ticker.history(period=history_period)
            if df.empty:
                return Response({"error": "No historical data found"}, status=404)

            df = df.reset_index()
            df['Date_Ordinal'] = df['Date'].apply(lambda x: x.toordinal())

            # Calculate historical daily volatility (Standard Deviation of daily price changes)
            # Use last 30 days of data to capture current regime
            daily_changes = df['Close'].diff().tail(30).dropna()
            volatility = daily_changes.std() if len(daily_changes) > 1 else 0.0

            X = df[['Date_Ordinal']].values
            y = df['Close'].values

            last_date = df['Date'].max()
            last_price = df['Close'].iloc[-1]
            future_dates = [last_date + timedelta(days=i) for i in range(1, days_to_predict + 1)]

            raw_future_preds = []

            if algorithm == "logistic":
                # Logistic Regression requires categorical labels.
                bins = np.linspace(df['Close'].min(), df['Close'].max(), 50)
                y_binned = np.digitize(y, bins)
                
                model = LogisticRegression(max_iter=1000)
                model.fit(X, y_binned)
                
                future_X = np.array([[last_date.toordinal() + i] for i in range(1, days_to_predict + 1)])
                pred_bins = model.predict(future_X)
                
                for b in pred_bins:
                    idx = min(max(b - 1, 0), len(bins) - 1)
                    # Add noise even to categorical prediction
                    noise = np.random.normal(0, volatility * 0.5) 
                    raw_future_preds.append(bins[idx] + noise)
            else:
                # Regressors (Linear, Ridge, Lasso)
                if algorithm == "ridge":
                    model = Ridge()
                elif algorithm == "lasso":
                    model = Lasso()
                else:
                    model = LinearRegression()
                    
                model.fit(X, y)
                slope = model.coef_[0]
                
                # Generate a Stochastic Random Walk with Drift
                current_sim_price = last_price
                for i in range(1, days_to_predict + 1):
                    # Drift + Brownian Noise
                    noise = np.random.normal(0, volatility)
                    current_sim_price = current_sim_price + slope + noise
                    raw_future_preds.append(current_sim_price)

            # Trajectory Smoothing: 3-day Simple Moving Average on the generated path
            # Buffer with last historical price for seamless transition
            path_for_smoothing = [last_price] + raw_future_preds
            future_preds = []
            
            for i in range(1, len(path_for_smoothing)):
                # Averaging window: [i-2, i-1, i] relative to the buffered path
                window = path_for_smoothing[max(0, i-2):i+1]
                future_preds.append(sum(window) / len(window))

            history = []
            for _, row in df.tail(30).iterrows(): # Return last 30 days for chart
                history.append({
                    "date": row['Date'].strftime("%Y-%m-%d"),
                    "price": round(row['Close'], 2),
                    "type": "historical"
                })

            predictions = []
            for d, p in zip(future_dates, future_preds):
                predictions.append({
                    "date": d.strftime("%Y-%m-%d"),
                    "price": round(float(p), 2),
                    "type": "predicted"
                })

            return Response({
                "symbol": yahoo_symbol,
                "algorithm": algorithm,
                "history": history,
                "predictions": predictions
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# -----------------------------
# 🧩 STOCK CLUSTERING API (K-Means)
# -----------------------------
class StockClusteringAPIView(APIView):
    def get(self, request):
        import os
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        
        portfolio_id = request.GET.get("portfolio_id")
        k = int(request.GET.get("k", 3))

        if not portfolio_id:
            return Response({"error": "portfolio_id required"}, status=400)

        from portfolio.models import Portfolio
        from stocks.models import PortfolioStock
        
        # Fetch stocks specifically for this portfolio
        stocks = PortfolioStock.objects.filter(portfolio_id=portfolio_id)
        if stocks.count() == 0:
            return Response({"error": "No stocks exist in this portfolio to perform clustering."}, status=400)

        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from itertools import combinations
        import pandas as pd
        import numpy as np
        
        # Build list including ALL duplicates
        data = []
        for s in stocks:
            data.append({
                "id": s.id,
                "symbol": str(s.stock.symbol).replace(".NS", ""),
                "current_price": float(s.current_price),
                "pe_ratio": float(s.pe_ratio),
                "discount_level": float(s.discount_level),
                "opportunity": float(s.opportunity)
            })

        df = pd.DataFrame(data)
        
        # We define the exact 4 features the user requested
        core_features = ["current_price", "pe_ratio", "discount_level", "opportunity"]
        
        # Generate all 2D combinations (6 pairs total)
        feature_pairs = list(combinations(core_features, 2))
        
        actual_k = min(k, len(df))
        results = []
        best_score = -1.0
        best_pair_idx = 0

        # Create human readable labels
        label_map = {
            "current_price": "Current Price",
            "pe_ratio": "P/E Ratio",
            "discount_level": "Discount Level",
            "opportunity": "Opportunity Score"
        }

        # Handle edge cases where silhouette scoring is scientifically impossible
        can_score = actual_k > 1 and len(df) > actual_k

        for idx, (f1, f2) in enumerate(feature_pairs):
            pair_features = [f1, f2]
            
            # Scale just these 2 features
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(df[pair_features])
            
            clusters = []
            score = 0.0

            if actual_k > 0:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    kmeans = KMeans(n_clusters=actual_k, random_state=42, n_init='auto')
                    cluster_labels = kmeans.fit_predict(scaled_features)
                    
                # Calculate silhouette score to determine clustering quality
                if can_score:
                    score = float(silhouette_score(scaled_features, cluster_labels))
                
                df_temp = df.copy()
                df_temp['cluster'] = cluster_labels
                
                for i in range(actual_k):
                    cluster_df = df_temp[df_temp['cluster'] == i]
                    cluster_stocks = []
                    
                    for _, row in cluster_df.iterrows():
                        cluster_stocks.append({
                            "id": int(row["id"]),
                            "symbol": str(row["symbol"]),
                            "x": float(row[f1]),
                            "y": float(row[f2])
                        })
                        
                    clusters.append({
                        "cluster_index": int(i),
                        "stocks": cluster_stocks
                    })
            else:
                clusters = []

            if score > best_score:
                best_score = score
                best_pair_idx = idx
                
            results.append({
                "pair_key": f"{f1}_vs_{f2}",
                "x_label": label_map[f1],
                "y_label": label_map[f2],
                "score": round(score, 3),
                "clusters": clusters
            })

        return Response({
            "portfolio_id": int(portfolio_id),
            "k": actual_k,
            "best_pair_idx": best_pair_idx,
            "pairs": results
        })

# -----------------------------
# 🌐 NIFTY 50 PCA CLUSTERING API
# -----------------------------
class Nifty50PCAAPIView(APIView):
    def get(self, request):
        import yfinance as yf
        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans
        import concurrent.futures

        # NIFTY 50 Tickers
        nifty50_tickers = [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
            "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "L&T.NS",
            "BAJFINANCE.NS", "HCLTECH.NS", "M&M.NS", "TATAMOTORS.NS", "MARUTI.NS",
            "SUNPHARMA.NS", "KOTAKBANK.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS",
            "TITAN.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "BAJAJFINSV.NS", "TATASTEEL.NS",
            "WIPRO.NS", "NESTLEIND.NS", "JSWSTEEL.NS", "TECHM.NS", "GRASIM.NS",
            "ADANIENT.NS", "HINDALCO.NS", "ADANIPORTS.NS", "DIVISLAB.NS", "BRITANNIA.NS",
            "APOLLOHOSP.NS", "CIPLA.NS", "SBILIFE.NS", "EICHERMOT.NS", "DRREDDY.NS",
            "TATACONSUM.NS", "BPCL.NS", "BAJAJ-AUTO.NS", "COALINDIA.NS", "INDUSINDBK.NS",
            "DABUR.NS", "SHREECEM.NS", "UPL.NS", "HEROMOTOCO.NS", "HDFCLIFE.NS"
        ]
        
        k = int(request.GET.get("k", 3))

        # 1. Fetch 1-Year Historical Prices efficiently in a single batch call
        try:
            hist_data = yf.download(nifty50_tickers, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)
        except Exception as e:
            return Response({"error": f"yfinance download failed: {str(e)}"}, status=500)

        # 2. Worker function to extract P/E, 52wk high, and current price per ticker
        def fetch_ticker_info(ticker):
            try:
                t = yf.Ticker(ticker)
                info = t.info
                
                # Try to get active price, else fallback to historical
                active_price = info.get("currentPrice", info.get("regularMarketPrice", None))
                pe = info.get("trailingPE", info.get("forwardPE", 15.0)) 
                fifty_two_high = info.get("fiftyTwoWeekHigh", active_price if active_price else 1)
                company_name = info.get("shortName", info.get("longName", ticker))
                
                return {
                    "symbol": ticker,
                    "company_name": company_name,
                    "current_price": active_price,
                    "pe_ratio": pe,
                    "max_price": fifty_two_high
                }
            except Exception:
                return None

        # Execute concurrent fetching
        ticker_info_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(fetch_ticker_info, nifty50_tickers)
            for res in results:
                if res:
                    ticker_info_list.append(res)

        # 3. Compile the 6 requested numerical features
        compiled_data = []

        for info in ticker_info_list:
            symbol = info['symbol']
            
            # yfinance returns MultiIndex if multiple tickers. Handle carefully.
            try:
                if isinstance(hist_data.columns, pd.MultiIndex):
                    closes = hist_data[symbol]['Close'].dropna()
                else:
                    closes = hist_data['Close'].dropna()
            except Exception:
                continue
                
            if len(closes) < 10:
                continue

            # Feature 1: Returns (1 Year) -> (Last / First) - 1
            annual_return = (closes.iloc[-1] / closes.iloc[0]) - 1

            # Feature 2: Volatility -> Annualized Standard Deviation of daily returns
            daily_returns = closes.pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)

            # Feature 3: Current Price
            curr_price = info['current_price'] if info['current_price'] else closes.iloc[-1]
                
            # Feature 4: P/E Ratio
            pe_ratio = info['pe_ratio'] if info['pe_ratio'] is not None else 15.0
            max_price = info['max_price'] if info['max_price'] else curr_price
            
            # Feature 5: Discount Level
            discount_level = 0.0
            if max_price and curr_price and max_price > 0:
                discount_level = max(0, ((max_price - curr_price) / max_price) * 100)
                
            # Feature 6: Opportunity Score (Discount Level / PE Ratio fallback)
            opportunity_score = discount_level / (pe_ratio if pe_ratio > 0 else 1)

            compiled_data.append({
                "symbol": symbol.replace(".NS", ""),
                "company_name": info.get("company_name", symbol),
                "returns": float(annual_return),
                "volatility": float(volatility),
                "current_price": float(curr_price),
                "pe_ratio": float(pe_ratio),
                "discount_level": float(discount_level),
                "opportunity": float(opportunity_score)
            })

        if not compiled_data:
            return Response({"error": "Failed to compile financial features for NIFTY 50."}, status=500)

        df = pd.DataFrame(compiled_data)

        # 4. Dimensionality Reduction (PCA)
        feature_cols = ["returns", "volatility", "current_price", "pe_ratio", "discount_level", "opportunity"]
        
        # Standard scale the 6D space
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(df[feature_cols])

        # PCA transformation to 2D
        pca = PCA(n_components=2, random_state=42)
        pca_result = pca.fit_transform(scaled_features)
        
        df['pc1'] = pca_result[:, 0]
        df['pc2'] = pca_result[:, 1]
        
        explained_variance = pca.explained_variance_ratio_

        # 5. K-Means Clustering
        actual_k = min(k, len(df))
        centroids = []
        if actual_k > 0:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                kmeans = KMeans(n_clusters=actual_k, random_state=42, n_init='auto')
                df['cluster'] = kmeans.fit_predict(pca_result)
                centroids = kmeans.cluster_centers_.tolist()
        else:
            df['cluster'] = 0

        # Construct payload mapping
        clusters = []
        for i in range(actual_k):
            cluster_df = df[df['cluster'] == i]
            cluster_stocks = []
            
            for _, row in cluster_df.iterrows():
                cluster_stocks.append({
                    "symbol": row["symbol"],
                    "company_name": row["company_name"],
                    "pc1": float(row["pc1"]),
                    "pc2": float(row["pc2"]),
                    "returns": float(row["returns"]),
                    "volatility": float(row["volatility"]),
                    "current_price": float(row["current_price"]),
                    "pe_ratio": float(row["pe_ratio"]),
                    "discount_level": float(row["discount_level"]),
                    "opportunity": float(row["opportunity"])
                })
                
            clusters.append({
                "cluster_index": i,
                "centroid_pc1": float(centroids[i][0]) if centroids else 0.0,
                "centroid_pc2": float(centroids[i][1]) if centroids else 0.0,
                "stocks": cluster_stocks
            })

        return Response({
            "k": actual_k,
            "variance_explained_pc1": round(float(explained_variance[0] * 100), 2),
            "variance_explained_pc2": round(float(explained_variance[1] * 100), 2),
            "clusters": clusters
        })


class PreciousMetalsAPIView(APIView):
    def get(self, request):
        import yfinance as yf
        import pandas as pd
        import numpy as np
        import concurrent.futures
        import shap
        from lime.lime_tabular import LimeTabularExplainer
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler

        precious_metals_tickers = [
            "GLD", "SLV", "IAU", "SGOL", "SIVR", "PPLT", "PALL", "GDX", "GDXJ", "SIL", 
            "SILJ", "NEM", "GOLD", "AEM", "FNV", "WPM", "KGC", "PAAS", "HL", "CDE",
            "AG", "FSM", "EXK", "EGO", "NGD", "SA", "AUY", "BTG", "IAG", "MAG",
            "SAND", "OR", "SSRM", "CGAU", "EQX", "OSK", "GFI", "AU", "HMY", "DRD"
        ]

        # 1. Fetch 1-Year Historical Prices
        try:
            hist_data = yf.download(precious_metals_tickers, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)
        except Exception as e:
            return Response({"error": f"yfinance download failed: {str(e)}"}, status=500)

        def fetch_ticker_info(ticker):
            try:
                t = yf.Ticker(ticker)
                info = t.info
                active_price = info.get("currentPrice", info.get("regularMarketPrice", None))
                pe = info.get("trailingPE", info.get("forwardPE", 15.0)) 
                fifty_two_high = info.get("fiftyTwoWeekHigh", active_price if active_price else 1)
                company_name = info.get("shortName", info.get("longName", ticker))
                
                return {
                    "symbol": ticker,
                    "company_name": company_name,
                    "current_price": active_price,
                    "pe_ratio": pe,
                    "max_price": fifty_two_high
                }
            except Exception:
                return None

        ticker_info_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(fetch_ticker_info, precious_metals_tickers)
            for res in results:
                if res:
                    ticker_info_list.append(res)
                    
        compiled_data = []
        portfolio_prices = {}
        target_returns = []

        for info in ticker_info_list:
            symbol = info['symbol']
            try:
                if isinstance(hist_data.columns, pd.MultiIndex):
                    closes = hist_data[symbol]['Close'].dropna()
                else:
                    closes = hist_data['Close'].dropna()
            except Exception:
                continue
                
            if len(closes) < 130:
                continue
                
            portfolio_prices[symbol] = closes

            annual_return = (closes.iloc[-1] / closes.iloc[0]) - 1
            momentum_6m = (closes.iloc[-1] / closes.iloc[-126]) - 1
            
            daily_returns = closes.pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)

            curr_price = info['current_price'] if info['current_price'] else closes.iloc[-1]
            pe_ratio = info['pe_ratio'] if info['pe_ratio'] is not None else 15.0
            max_price = info['max_price'] if info['max_price'] else curr_price
            
            discount_level = 0.0
            if max_price and curr_price and max_price > 0:
                discount_level = max(0, ((max_price - curr_price) / max_price) * 100)
                
            opportunity_score = discount_level / (pe_ratio if pe_ratio > 0 else 1)

            target = (closes.iloc[-1] / closes.iloc[-21]) - 1

            compiled_data.append({
                "symbol": symbol,
                "company_name": info.get("company_name", symbol),
                "returns": float(annual_return),
                "volatility": float(volatility),
                "momentum": float(momentum_6m),
                "pe_ratio": float(pe_ratio),
                "discount_level": float(discount_level),
                "opportunity": float(opportunity_score),
                "current_price": float(curr_price)
            })
            target_returns.append(target)
            
        if not compiled_data:
            return Response({"error": "Failed to compile precious metals data."}, status=500)

        df = pd.DataFrame(compiled_data)
        
        common_index = None
        for sym, closes in portfolio_prices.items():
            if common_index is None:
                common_index = closes.index
            else:
                common_index = common_index.intersection(closes.index)
                
        if len(common_index) > 0:
            growth_df = pd.DataFrame(index=common_index)
            for sym, closes in portfolio_prices.items():
                if sym in df['symbol'].values:
                    growth_df[sym] = closes.reindex(common_index)
            
            growth_df = growth_df / growth_df.iloc[0]
            portfolio_value = growth_df.mean(axis=1) * 10000
            
            portfolio_growth_series = []
            for date, val in portfolio_value.items():
                portfolio_growth_series.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "value": float(val)
                })
        else:
            portfolio_growth_series = []
            
        feature_cols = ["returns", "volatility", "momentum", "pe_ratio", "opportunity"]
        X = df[feature_cols]
        y = np.array(target_returns)
        
        imputer = SimpleImputer(strategy='median')
        X_imputed = imputer.fit_transform(X)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)
        
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_scaled)
        
        shap_importance = np.mean(np.abs(shap_values), axis=0)
        shap_data = []
        for i, col in enumerate(feature_cols):
            shap_data.append({
                "feature": col.capitalize(),
                "importance": float(shap_importance[i]) * 100
            })
            
        shap_data.sort(key=lambda x: x["importance"], reverse=True)
        
        lime_target_idx = 0
        target_sym = "NEM"
        if target_sym in df['symbol'].values:
            lime_target_idx = df[df['symbol'] == target_sym].index[0]
        elif len(df) > 0:
            lime_target_idx = 0
            
        target_instance = X_scaled[lime_target_idx]
        target_company = df.iloc[lime_target_idx]['company_name']
        
        lime_explainer = LimeTabularExplainer(
            X_scaled,
            feature_names=feature_cols,
            class_names=['1M_Return'],
            mode='regression',
            random_state=42
        )
        
        lime_exp = lime_explainer.explain_instance(
            target_instance, 
            model.predict, 
            num_features=5
        )
        
        lime_data_raw = lime_exp.as_list()
        lime_data = []
        for feature_desc, weight in lime_data_raw:
            detected_feature = "Unknown"
            for col in feature_cols:
                if col in feature_desc:
                    detected_feature = col.capitalize()
                    break
                    
            lime_data.append({
                "feature": detected_feature,
                "contribution": float(weight) * 100 
            })

        # --- Outlier Control for Scatter Plot ---
        # Cap P/E Ratio and Opportunity Score to prevent extreme outliers from compressing the chart
        vm_df = df.copy()
        
        pe_90th = vm_df['pe_ratio'].quantile(0.90)
        opp_90th = vm_df['opportunity'].quantile(0.90)
        
        vm_df['pe_ratio'] = np.clip(vm_df['pe_ratio'], 0, pe_90th)
        vm_df['opportunity'] = np.clip(vm_df['opportunity'], 0, opp_90th)
        # ----------------------------------------

        return Response({
            "value_matrix_data": vm_df.to_dict('records'),
            "portfolio_growth_series": portfolio_growth_series,
            "shap_data": shap_data,
            "lime_data": {
                "asset": target_company,
                "explanations": lime_data
            }
        })

class CryptoForecastingAPIView(APIView):
    def get(self, request):
        import yfinance as yf
        import pandas as pd
        from datetime import timedelta
        try:
            horizon_str = request.query_params.get('horizon', '30')
            selected_asset = request.query_params.get('symbol', 'BTC-USD').upper()
            
            # Asset to Ticker Mapping
            asset_map = {
                "BITCOIN": "BTC-USD",
                "BTC-USD": "BTC-USD",
                "GOLD": "GC=F",
                "SILVER": "SI=F",
                "RGD STOCKS": "RGD.TO",
                "RGD": "RGD.TO"
            }
            
            ticker_symbol = asset_map.get(selected_asset, selected_asset)
            
            try:
                horizon = int(horizon_str)
            except ValueError:
                horizon = 30
                
            if horizon not in [7, 30, 90]:
                horizon = 30

            # 1. Fetch live historical data from yfinance
            asset_ticker = yf.Ticker(ticker_symbol)
            # Fetch 2 years of daily data to ensure reliable ARIMA training
            df = asset_ticker.history(period="2y")
            
            if df.empty:
                return Response({"error": f"Failed to fetch data for {ticker_symbol}."}, status=500)
                
            df.index = df.index.tz_localize(None)
            closes = df['Close'].dropna()

            # 2. Time Series Preprocessing
            # Resample to daily frequency. Crypto is 24/7, Commodities/Stocks are 5 days.
            # Using 'D' resample with forward fill to handle weekends and market holidays.
            closes = closes.resample('D').ffill()

            # 3. Model Training
            from statsmodels.tsa.arima.model import ARIMA
            import numpy as np
            
            # Using ARIMA with trend='t' (drift) to capture overall directional momentum
            model = ARIMA(closes, order=(5, 1, 0), trend='t')
            model_fit = model.fit()

            # 4. Forecasting the Mean Expected Value
            forecast_obj = model_fit.get_forecast(steps=horizon)
            forecast_mean = forecast_obj.predicted_mean
            
            # 4b. Injecting Realism via Stochastic Simulation
            recent_volatility = np.std(closes.diff().dropna()[-30:])
            
            # Stable seed based on horizon and ticker to prevent wild jitter
            np.random.seed(42 + horizon + hash(ticker_symbol) % 1000) 
            
            daily_shock = np.random.normal(0, recent_volatility * 0.7, horizon)
            stochastic_path = forecast_mean.values + np.cumsum(daily_shock)

            # 5. Serialization for Frontend visualization (Recharts)
            
            # Show last 90 days for visual context
            recent_history = closes.iloc[-90:]
            
            historical_data = []
            for date, price in recent_history.items():
                historical_data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "historical_price": float(price),
                    "predicted_price": None 
                })
                
            forecast_data = []
            # Seamless transition
            last_date = recent_history.index[-1]
            last_price = recent_history.iloc[-1]
            forecast_data.append({
                "date": last_date.strftime('%Y-%m-%d'),
                "historical_price": None,
                "predicted_price": float(last_price)
            })
            
            for i, (date, _) in enumerate(forecast_mean.items()):
                forecast_data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "historical_price": None,
                    "predicted_price": float(stochastic_path[i])
                })

            return Response({
                "symbol": ticker_symbol,
                "asset_name": selected_asset,
                "horizon": horizon,
                "data": historical_data + forecast_data
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)
