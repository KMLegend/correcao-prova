import { useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ResultsTable from "./components/ResultsTable";

function App() {
  const [results, setResults] = useState(null);

  const handleCorrection = (data) => {
    setResults(data);
    // Smooth scroll to results
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }, 100);
  };

  return (
    <div className="min-height-screen bg-slate-50 pb-20">
      <Header />
      
      <main className="container mx-auto px-4 pt-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-extrabold text-slate-800 mb-4">
            Corrija provas em segundos com Visão Computacional
          </h2>
          <p className="text-slate-600 text-lg max-w-2xl mx-auto">
            Faça upload do gabarito oficial e do cartão-resposta digitalizado para obter 
            os resultados instantaneamente com nossa tecnologia de reconhecimento de marcas.
          </p>
        </div>

        <UploadSection onCorrection={handleCorrection} />
        
        {results && <ResultsTable results={results} />}
      </main>

      <footer className="mt-20 text-center text-slate-400 text-sm">
        <p>&copy; 2026 Sistema de Correção Automática de Provas - Projeto Integrador</p>
      </footer>
    </div>
  );
}

export default App;
