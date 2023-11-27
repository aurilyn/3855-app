import React, { useState, useEffect } from 'react';

const HealthCheck = () => {
    const [healthStatus, setHealthStatus] = useState('');  // State to store health status

    fetch(`http://benny-3855.eastus2.cloudapp.azure.com/health/health`)
        .then(res => res.json())
        .then((result)=>{
            console.log("Received Stats")
            setStats(result);
            setIsLoaded(true);
        },(error) =>{
            setError(error)
            setIsLoaded(true);
    })

    return (
        <div>
            <h2>Health Check</h2>
            <p>Status: {healthStatus}</p>
        </div>
    );
};

export default HealthCheck;