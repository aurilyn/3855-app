import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`benny-3855.eastus2.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Augment</th>
							<th>Champion</th>
						</tr>
						<tr>
							<td># Total Augment: {stats['total_augment']}</td>
							<td># Total Champion: {stats['total_unit']}</td>
						</tr>
						<tr>
							<td colspan="2">Min Augment Placement: {stats['lowest_augment_placement']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Champion Cost: {stats['highest_champion_cost']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Augment Placement: {stats['highest_augment_placement']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
