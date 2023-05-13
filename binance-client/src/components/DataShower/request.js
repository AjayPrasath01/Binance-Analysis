import axios from "../../axios";

export const getData = (setData, setDataFetchStatus, navigate) => {
	axios
		.get("/api/data/fetch/all/")
		.then((res) => {
			setData(res.data.data);
			setDataFetchStatus("DONE");
		})
		.catch((error) => {
			if (error?.response?.status === 401) {
				navigate("/");
			}
			console.log(error);
		});
};

export const logout = (navigate) => {
	axios
		.get("/api/logout/")
		.then(() => {
			navigate("/");
		})
		.catch(() => {
			console.log("Some thing when wrong");
		});
};
