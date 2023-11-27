import React, { useState, useEffect } from 'react';

const HealthCheck = () => {
    const [healthStatus, setHealthStatus] = useState('');  // State to store health status

    const getHealth = () => {
        fetch(`http://benny-3855.eastus2.cloudapp.azure.com/health/health`)
            .then(res => res.json())
            .then((result)=>{
                console.log("Received Stats")
                setHealthStatus(result);
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
            <p>{healthStatus}</p>
        </div>
    );
};

export default HealthCheck;