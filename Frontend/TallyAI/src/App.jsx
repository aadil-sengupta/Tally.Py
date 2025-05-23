import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ChatPage from './pages/ChatPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ChatPage />} />
          <Route path="chat/:chatId" element={<ChatPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;