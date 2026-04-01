export default function Header() {
  return (
    <header className="bg-indigo-700 text-white p-6 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Correção de Provas</h1>
          <p className="text-sm opacity-80 mt-1 uppercase tracking-wider">Sistema OCR / OMR</p>
        </div>
        <div className="hidden md:block">
          <span className="bg-indigo-600 px-4 py-2 rounded-lg text-sm font-medium border border-indigo-500">
            Faculdade Digital
          </span>
        </div>
      </div>
    </header>
  );
}
