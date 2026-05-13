import React, { useState } from 'react';

const CRUDForm = ({ initialValues, onSubmit }) => {
    const [formData, setFormData] = useState(initialValues || {});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            {Object.keys(formData).map((field) => (
                <div key={field}>
                    <label>{field}</label>
                    <input
                        type="text"
                        name={field}
                        value={formData[field]}
                        onChange={handleChange}
                    />
                </div>
            ))}
            <button type="submit">Submit</button>
        </form>
    );
};

export default CRUDForm;