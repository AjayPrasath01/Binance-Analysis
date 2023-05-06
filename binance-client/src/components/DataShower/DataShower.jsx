import React, { useEffect, useState } from "react";
import "./DataShower.css";
import { getAllRsd } from "./request";

function DataShower() {
	const [rsdData, setRsdData] = useState({});
	const [dataFetchStatus, setDataFetchStatus] = useState("PROCESSING");

	useEffect(() => {
		getAllRsd(setRsdData, setDataFetchStatus);
	}, []);

	return (
		<div>
			{console.log(Object.keys(rsdData))}
			{Object.keys(rsdData).map((key) => {
				return (
					<div className="card">
						<span className="symbol">{key}</span>
						<span className="rsd">
							{rsdData[key] ? rsdData[key].toFixed(2) : "Not Available"}
						</span>
					</div>
				);
			})}
		</div>
	);
}

export default DataShower;
