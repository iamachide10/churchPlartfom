import { Main } from "./Pages/Main";
import { SermonListPage } from "./Pages/SermonListPage";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import UploadSermon from "./Pages/UploadSermon";


const App = () => {


  return(
    <>
    <AuthProvider>
    <BrowserRouter>
    {/* <UploadSermon/> */}
    <Main/>
    </BrowserRouter>
    </AuthProvider>
    </>
  )
}
export default App;