import { useState } from "react";

export default function UploadSection({ onCorrection }) {
  const [gabarito, setGabarito] = useState(null);
  const [cartao, setCartao] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!gabarito || !cartao) {
      setError("Por favor, selecione ambos os arquivos (Gabarito e Cartão-Resposta).");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("gabarito", gabarito);
    formData.append("cartao", cartao);

    try {
      // Usando fetch nativo conforme sugerido na doc (ou axios se preferir)
      const response = await fetch("/api/corrigir", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = "Erro ao processar as imagens.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) { /* fallback case */ }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      onCorrection(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-8 bg-white p-8 rounded-2xl shadow-xl max-w-2xl mx-auto border border-gray-100">
      <h2 className="text-2xl font-bold mb-8 text-gray-800 flex items-center">
        <span className="bg-indigo-100 text-indigo-700 w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">1</span>
        Upload de Arquivos
      </h2>
      
      <form onSubmit={handleUpload} className="space-y-8">
        <div className="grid grid-cols-1 gap-6">
          <div className="group">
            <label className="block text-sm font-semibold text-gray-700 mb-2 group-hover:text-indigo-600 transition-colors">
              Gabarito Oficial (Imagem)
            </label>
            <div className="relative">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setGabarito(e.target.files[0])}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-all cursor-pointer border-2 border-dashed border-gray-200 rounded-xl p-2 hover:border-indigo-300 focus:outline-none"
              />
              {gabarito && <p className="mt-2 text-xs text-green-600 font-medium">✓ {gabarito.name}</p>}
            </div>
          </div>

          <div className="group">
            <label className="block text-sm font-semibold text-gray-700 mb-2 group-hover:text-indigo-600 transition-colors">
              Cartão-Resposta do Aluno (Imagem)
            </label>
            <div className="relative">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setCartao(e.target.files[0])}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-all cursor-pointer border-2 border-dashed border-gray-200 rounded-xl p-2 hover:border-indigo-300 focus:outline-none"
              />
              {cartao && <p className="mt-2 text-xs text-green-600 font-medium">✓ {cartao.name}</p>}
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-xl border border-red-100 text-sm animate-pulse">
            <strong>Erro:</strong> {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-4 px-6 rounded-xl text-white font-bold text-lg transition-all transform ${
            loading 
              ? "bg-gray-400 cursor-not-allowed" 
              : "bg-indigo-600 hover:bg-indigo-700 active:scale-95 shadow-lg hover:shadow-indigo-200"
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processando Imagens...
            </span>
          ) : "Iniciar Correção Automática"}
        </button>
      </form>
    </div>
  );
}
