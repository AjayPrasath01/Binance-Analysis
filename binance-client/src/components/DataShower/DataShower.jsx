import React, { useEffect, useState } from "react";
import "./DataShower.css";
import { getData, logout } from "./request";
import Card from "./Card";
import { useNavigate } from "react-router-dom";

function DataShower() {
	const [data, setData] = useState([]);
	const navigate = useNavigate();
	const [dataFetchStatus, setDataFetchStatus] = useState("PROCESSING");

	const handleLogout = () => {
		logout(navigate);
	};

	useEffect(() => {
		getData(setData, setDataFetchStatus, navigate);
	}, []);
	return (
		<div className="table-container">
			<button className="button logout" onClick={handleLogout}>
				Logout
			</button>
			<h1 className="subtitle">Demystifying Bitcoin</h1>
			{data.length > 0 &&
				data.map((element, index) => {
					if (element["symbol"] === "BTCUSD") {
						return (
							<div
								key={index}
								className="card"
								style={{
									position: "sticky",
									top: "0px",
									borderTopRightRadius: "10px",
									borderTopLeftRadius: "10px",
								}}
							>
								<span>
									<span
										className="symbol"
										style={{ fontWeight: "bolder", fontSize: "larger" }}
									>
										SYMBOL
									</span>
									<span
										className="close_date_time"
										style={{ fontWeight: "bolder", fontSize: "larger" }}
									>
										CLOSE DATE TIME
									</span>
								</span>
								<>
									<span
										className="rsd"
										style={{ fontWeight: "bolder", fontSize: "larger" }}
									>
										RSMA
									</span>
									<span
										className="rsd"
										style={{ fontWeight: "bolder", fontSize: "larger" }}
									>
										RSMA 200
									</span>
									<span
										className="rsd"
										style={{ fontWeight: "bolder", fontSize: "larger" }}
									>
										RSD
									</span>
								</>
							</div>
						);
					}
					return <Card key={index} index={index} element={element} />;
				})}
			<div className="bottom-span"></div>
		</div>
	);
}

export default DataShower;
