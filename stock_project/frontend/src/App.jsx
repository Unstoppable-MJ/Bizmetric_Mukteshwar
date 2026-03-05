import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PortfolioDetails from "./pages/PortfolioDetails";
import Nifty50PCA from "./pages/Nifty50PCA";
import PreciousMetalsPortfolio from "./pages/PreciousMetalsPortfolio";
import CryptoPortfolio from "./pages/CryptoPortfolio";
import MainLayout from "./layouts/MainLayout";
import { useState, useEffect } from "react";
import API from "./services/api";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [portfolios, setPortfolios] = useState([]);
  const [activePortfolio, setActivePortfolio] = useState("");

  const fetchPortfolios = () => {
    API.get("portfolios/")
      .then((res) => {
        setPortfolios(res.data);
        if (res.data.length > 0 && !activePortfolio) {
          setActivePortfolio(res.data[0].id);
        }
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchPortfolios();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const refreshData = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <MainLayout
              refreshData={refreshData}
              portfolios={portfolios}
              activePortfolio={activePortfolio}
              setActivePortfolio={setActivePortfolio}
              fetchPortfolios={fetchPortfolios}
            >
              <Dashboard key={`${refreshKey}-${activePortfolio}`} activePortfolio={activePortfolio} />
            </MainLayout>
          }
        />
        <Route
          path="/portfolio-details"
          element={
            <MainLayout
              refreshData={refreshData}
              portfolios={portfolios}
              activePortfolio={activePortfolio}
              setActivePortfolio={setActivePortfolio}
              fetchPortfolios={fetchPortfolios}
            >
              <PortfolioDetails key={`details-${refreshKey}-${activePortfolio}`} activePortfolio={activePortfolio} />
            </MainLayout>
          }
        />
        <Route
          path="/nifty50-pca"
          element={
            <MainLayout
              refreshData={refreshData}
              portfolios={portfolios}
              activePortfolio={activePortfolio}
              setActivePortfolio={setActivePortfolio}
              fetchPortfolios={fetchPortfolios}
            >
              <Nifty50PCA />
            </MainLayout>
          }
        />
        <Route
          path="/precious-metals"
          element={
            <MainLayout
              refreshData={refreshData}
              portfolios={portfolios}
              activePortfolio={activePortfolio}
              setActivePortfolio={setActivePortfolio}
              fetchPortfolios={fetchPortfolios}
            >
              <PreciousMetalsPortfolio />
            </MainLayout>
          }
        />
        <Route
          path="/crypto-ai"
          element={
            <MainLayout
              refreshData={refreshData}
              portfolios={portfolios}
              activePortfolio={activePortfolio}
              setActivePortfolio={setActivePortfolio}
              fetchPortfolios={fetchPortfolios}
            >
              <CryptoPortfolio />
            </MainLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;