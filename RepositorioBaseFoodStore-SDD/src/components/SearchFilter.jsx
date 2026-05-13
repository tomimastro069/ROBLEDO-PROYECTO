import React, { useState } from 'react';

const SearchFilter = ({ onFilter }) => {
    const [query, setQuery] = useState('');

    const handleInputChange = (e) => {
        const value = e.target.value;
        setQuery(value);
        debounce(() => onFilter(value), 300)();
    };

    const debounce = (func, wait) => {
        let timeout;
        return () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(), wait);
        };
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search..."
                value={query}
                onChange={handleInputChange}
            />
        </div>
    );
};

export default SearchFilter;