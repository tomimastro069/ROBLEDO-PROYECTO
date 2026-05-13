import React from 'react';

const TableComponent = ({ data, columns, onSort, currentPage, totalPages, onPageChange }) => {
    return (
        <div>
            <table>
                <thead>
                    <tr>
                        {columns.map((col) => (
                            <th key={col.field} onClick={() => onSort(col.field)}>
                                {col.label}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index}>
                            {columns.map((col) => (
                                <td key={col.field}>{row[col.field]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div>
                <button disabled={currentPage === 1} onClick={() => onPageChange(currentPage - 1)}>
                    Previous
                </button>
                <span>{`${currentPage} / ${totalPages}`}</span>
                <button disabled={currentPage === totalPages} onClick={() => onPageChange(currentPage + 1)}>
                    Next
                </button>
            </div>
        </div>
    );
};

export default TableComponent;