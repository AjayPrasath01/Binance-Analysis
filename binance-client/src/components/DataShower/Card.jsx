import React from "react";

function Card({ index, element }) {
	return (
		<div className="card" style={index % 2 ? {backgroundColor: "#eeeeee"} : undefined}>
			<span>
				<span className="symbol">{element["symbol"]}</span>
				<span className="close_date_time">
					{new Date(element["close_date_time"]).toLocaleString()}
				</span>
			</span>
			{element["rsd"] ? (
				<>
					<span className="rsd">{parseFloat(element["rsma"]).toFixed(9)}</span>
					<span className="rsd">
						{parseFloat(element["rsma_200"]).toFixed(9)}
					</span>
					<span className="rsd">{parseFloat(element["rsd"]).toFixed(2)}</span>
				</>
			) : (
				<span className="promt"> No Enough data points </span>
			)}
		</div>
	);
}

export default Card;
