import { Main } from "./Pages/Main";
import { SermonListPage } from "./Pages/SermonListPage";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";


const App = () => {


  return(
    <>
    <AuthProvider>
    <BrowserRouter>
    <Main/>
    </BrowserRouter>
    </AuthProvider>
    </>
  )
}
export default App;