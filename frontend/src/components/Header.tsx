const Header = () => {
  return (
    <header className="w-full bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center">
        <img
          src="/realitech-logo.svg"
          alt="Realitech"
          className="h-10 w-auto"
        />
        <h1 className="ml-6 text-2xl font-semibold text-gray-800">
          Stream-View
        </h1>
      </div>
    </header>
  );
};

export default Header;
