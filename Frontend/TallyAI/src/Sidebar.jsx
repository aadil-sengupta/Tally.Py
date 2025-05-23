const Sidebar = () => {
  const pastChats = [
    { id: '1', title: 'Fetching Vouchers from United Way' },
    { id: '2', title: 'GST Form Filing' },
    { id: '3', title: 'Accounting 101' },
  ];

  return (
    <aside className="w-64 bg-gray-800 p-4 space-y-4 overflow-y-auto">
      <h2 className="text-xl font-semibold mb-4">Past Chats</h2>
      <nav>
        <ul>
          {pastChats.map((chat) => (
            <li key={chat.id} className="mb-2">
              <a
                href={`/chat/${chat.id}`} 
                className="block p-2 rounded hover:bg-gray-700 transition-colors"
              >
                {chat.title}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <button className="w-full mt-4 p-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors">
        + New Chat
      </button>
    </aside>
  );
};

export default Sidebar;