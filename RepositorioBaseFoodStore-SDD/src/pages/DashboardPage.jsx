import React, { useEffect, useState } from 'react';
import TableComponent from '../components/TableComponent';
import CRUDForm from '../components/CRUDForm';
import DeleteConfirmation from '../components/DeleteConfirmation';
import SearchFilter from '../components/SearchFilter';
import SnackbarNotification from '../components/SnackbarNotification';
import axios from 'axios';

const DashboardPage = () => {
    const [records, setRecords] = useState([]);
    const [selectedRecord, setSelectedRecord] = useState(null);
    const [snackbar, setSnackbar] = useState({ message: '', type: '' });
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        fetchRecords();
    }, [currentPage]);

    const fetchRecords = async () => {
        try {
            const response = await axios.get(`/api/records?page=${currentPage}`);
            setRecords(response.data.records);
            setTotalPages(response.data.totalPages);
        } catch (error) {
            setSnackbar({ message: 'Failed to fetch records', type: 'error' });
        }
    };

    const handleCreateOrUpdate = async (data) => {
        try {
            if (data.id) {
                await axios.put(`/api/records/${data.id}`, data);
                setSnackbar({ message: 'Record updated successfully', type: 'success' });
            } else {
                await axios.post('/api/records', data);
                setSnackbar({ message: 'Record created successfully', type: 'success' });
            }
            fetchRecords();
        } catch (error) {
            setSnackbar({ message: 'Failed to save record', type: 'error' });
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`/api/records/${id}`);
            setSnackbar({ message: 'Record deleted successfully', type: 'success' });
            fetchRecords();
        } catch (error) {
            setSnackbar({ message: 'Failed to delete record', type: 'error' });
        }
    };

    const handleSearch = async (query) => {
        try {
            const response = await axios.get(`/api/records?search=${query}`);
            setRecords(response.data.records);
            setTotalPages(response.data.totalPages);
        } catch (error) {
            setSnackbar({ message: 'Failed to search records', type: 'error' });
        }
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <SearchFilter onFilter={handleSearch} />
            <TableComponent
                data={records}
                columns={[
                    { field: 'id', label: 'ID' },
                    { field: 'name', label: 'Name' },
                    { field: 'email', label: 'Email' },
                ]}
                onSort={(field) => console.log('Sort by:', field)}
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
            />
            <CRUDForm
                initialValues={selectedRecord || {}}
                onSubmit={handleCreateOrUpdate}
            />
            <DeleteConfirmation
                onConfirm={() => handleDelete(selectedRecord?.id)}
                onCancel={() => setSelectedRecord(null)}
            />
            <SnackbarNotification
                message={snackbar.message}
                type={snackbar.type}
                onClose={() => setSnackbar({ message: '', type: '' })}
            />
        </div>
    );
};

export default DashboardPage;