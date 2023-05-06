import axios from "../../axios";

export const getAllRsd = (setRsdData, setDataFetchStatus) => {
	axios
		.get("/api/data/fetch/all/")
		.then((res) => {
			setRsdData(res.data);
			setDataFetchStatus("DONE");
		})
		.catch((error) => {
			console.log(error);
		});
};
