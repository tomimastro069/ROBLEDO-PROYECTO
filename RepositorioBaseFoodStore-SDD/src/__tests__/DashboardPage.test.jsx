import { render, screen, fireEvent } from '@testing-library/react';
import DashboardPage from '../pages/DashboardPage';
import axios from 'axios';

jest.mock('axios');

describe('DashboardPage', () => {
    test('renders the dashboard with table and components', async () => {
        axios.get.mockResolvedValue({
            data: { records: [{ id: 1, name: 'John', email: 'john@example.com' }], totalPages: 1 },
        });

        render(<DashboardPage />);

        const title = screen.getByText(/Dashboard/i);
        expect(title).toBeInTheDocument();

        const tableHeaders = screen.getAllByRole('columnheader');
        expect(tableHeaders.length).toBeGreaterThan(0);

        const createButton = screen.getByRole('button', { name: /submit/i });
        expect(createButton).toBeInTheDocument();
    });

    test('handles search with API call', async () => {
        axios.get.mockResolvedValue({ data: { records: [], totalPages: 0 } });

        render(<DashboardPage />);

        const searchBox = screen.getByPlaceholderText(/Search.../i);
        fireEvent.change(searchBox, { target: { value: 'query' } });

        expect(axios.get).toHaveBeenCalledWith('/api/records?search=query');
    });

    test('handles create/update with API call', async () => {
        axios.post.mockResolvedValue({});

        render(<DashboardPage />);

        const createButton = screen.getByRole('button', { name: /submit/i });
        fireEvent.click(createButton);

        expect(axios.post).toHaveBeenCalled();
    });
});