import axios from "axios";
export const SERVER = undefined;

export default axios.create({
	baseURL: SERVER,
	timeout: 15000,
	withCredentials: true
});
