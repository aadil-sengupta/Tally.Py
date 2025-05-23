const ChatPage = () => {
  return (
    <div className="flex flex-col h-full">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-gray-100">Chat Interface</h1>
      </header>
      

      <div className="flex-1 bg-gray-800 p-4 rounded-lg shadow mb-4 overflow-y-auto">
        <div className="text-gray-400">No messages yet. Start typing below!</div>
        {/* 
        <div className="mb-2 text-right">
          <span className="inline-block bg-blue-600 text-white p-2 rounded-lg">Hello!</span>
        </div>
        <div className="mb-2 text-left">
          <span className="inline-block bg-gray-700 text-gray-200 p-2 rounded-lg">Hi there! How can I help?</span>
        </div>
        */}
      </div>
      
      <div className="mt-auto bg-gray-800 p-4 rounded-lg shadow">
        <div className="flex items-center">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 p-3 bg-gray-700 text-gray-200 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-r-lg transition-colors">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;