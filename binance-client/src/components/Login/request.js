import axios from "../../axios";

export const submitLogin = (username, password, errorElement, navigate) => {
	axios
		.post("/api/login/", { username, password })
		.then(() => {
			navigate("/data");
		})
		.catch((error) => {
			if (error.response.status === 401) {
				const element = document.getElementById("error-text");
				element.style.display = "block";
				if (error.response?.data?.message) {
					element.innerText = error.response.data.message;
				} else {
					element.innerText = "Something when wrong";
				}
			}
		});
};
