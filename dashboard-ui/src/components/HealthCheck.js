import React, { useState, useEffect } from 'react';

const HealthCheck = () => {
    const [healthStatus, setHealthStatus] = useState('');  // State to store health status
    const [error, setError] = useState(null);

    const getHealth = () => {
        fetch(`http://benny-3855.eastus2.cloudapp.azure.com/health/health`)
            .then(res => res.json())
            .then((result)=>{
                console.log("Received Stats")
                setHealthStatus(result);
                setError(null); 
            },(error) =>{
                setError(error)
        })
    }

    useEffect(() => {
		const interval = setInterval(() => getHealth(), 20000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getHealth]);

    return (
        <div>
            <h2>Health Check</h2>
            {error ? (
                <p>Error fetching data: {error.message}</p>
            ) : (
                <div>
                    <p>Audit: {healthStatus.audit}</p>
                    <p>Processing: {healthStatus.processing}</p>
                    <p>Receiver: {healthStatus.receiver}</p>
                    <p>Storage: {healthStatus.storage}</p>
                    <p>Last Updated: {healthStatus.last_updated}</p>
                </div>
            )}
        </div>
    );
};

export default HealthCheck;