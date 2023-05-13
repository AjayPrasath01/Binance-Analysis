import "./App.css";
import DataShower from "./components/DataShower/DataShower";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login/Login";

function App() {
	return (
		<Router>
			<Routes>
				<Route exact path="/data" element={<DataShower />} />
				<Route exact path="/" element={<Login />} />
			</Routes>
		</Router>
	);
}

export default App;
