import React, { useState } from 'react';
import { Search } from 'lucide-react';

const TrainForm = ({ onSearch, isLoading }) => {
    const [trainNo, setTrainNo] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (trainNo.trim()) {
            onSearch(trainNo.trim());
        }
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className="train-form">
                <div className="input-wrapper">
                    <input
                        type="text"
                        placeholder="Enter Train Number (e.g., 12051)"
                        value={trainNo}
                        onChange={(e) => setTrainNo(e.target.value)}
                        disabled={isLoading}
                        className="train-input"
                        autoFocus
                    />
                    <button type="submit" disabled={isLoading || !trainNo.trim()} className={`submit-button ${isLoading ? 'loading' : ''}`}>
                        {isLoading ? (
                            <>
                                <div className="spinner-small"></div>
                                <span>Fetching...</span>
                            </>
                        ) : (
                            <>
                                <Search size={20} />
                                <span>Check Status</span>
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default TrainForm;
