import React, { useState, useEffect } from 'react';

const SnackbarNotification = ({ message, type, onClose }) => {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (message) {
            setVisible(true);
            const timer = setTimeout(() => {
                setVisible(false);
                onClose();
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [message, onClose]);

    if (!visible) return null;

    return (
        <div className={`snackbar ${type}`}>
            {message}
        </div>
    );
};

export default SnackbarNotification;