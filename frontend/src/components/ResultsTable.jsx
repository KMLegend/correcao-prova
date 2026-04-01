export default function ResultsTable({ results }) {
  if (!results) return null;

  return (
    <div className="mt-12 bg-white p-8 rounded-2xl shadow-xl max-w-4xl mx-auto border border-gray-100 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <h2 className="text-2xl font-bold mb-8 text-gray-800 flex items-center">
        <span className="bg-indigo-100 text-indigo-700 w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">2</span>
        Resultado da Correção
      </h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
        <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 flex flex-col items-center justify-center">
          <span className="text-xs text-slate-500 uppercase font-bold tracking-widest mb-1 text-center">Questões</span>
          <span className="text-3xl font-black text-slate-800">{results.resumo.total_questoes}</span>
        </div>
        <div className="bg-emerald-50 p-6 rounded-2xl border border-emerald-100 flex flex-col items-center justify-center">
          <span className="text-xs text-emerald-600 uppercase font-bold tracking-widest mb-1 text-center">Acertos</span>
          <span className="text-3xl font-black text-emerald-700">{results.resumo.acertos}</span>
        </div>
        <div className="bg-rose-50 p-6 rounded-2xl border border-rose-100 flex flex-col items-center justify-center">
          <span className="text-xs text-rose-600 uppercase font-bold tracking-widest mb-1 text-center">Erros</span>
          <span className="text-3xl font-black text-rose-700">{results.resumo.erros}</span>
        </div>
        <div className="bg-indigo-50 p-6 rounded-2xl border border-indigo-100 flex flex-col items-center justify-center transition-transform hover:scale-105">
          <span className="text-xs text-indigo-600 uppercase font-bold tracking-widest mb-1 text-center">Nota Final</span>
          <span className="text-4xl font-black text-indigo-800 leading-none">{results.resumo.nota}</span>
          <span className="text-xs text-indigo-400 mt-1">de 10.0</span>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-gray-100">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest">Questão</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest">Resposta do Aluno</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest">Gabarito</th>
              <th className="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest">Aproveitamento</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {results.detalhes.map((r, i) => (
              <tr key={i} className="hover:bg-indigo-50/30 transition-colors group">
                <td className="px-6 py-5 whitespace-nowrap text-sm font-bold text-gray-900">
                  {String(r.questao).padStart(2, '0')}
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-sm text-gray-600 font-medium">
                  {r.resposta_aluno}
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-sm text-gray-600 font-medium">
                  {r.resposta_correta}
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <span className={`px-4 py-1.5 inline-flex text-xs leading-5 font-bold rounded-full uppercase tracking-tighter ${
                    r.status === "Acerto" 
                      ? "bg-emerald-100 text-emerald-800 shadow-sm shadow-emerald-100" 
                      : "bg-rose-100 text-rose-800 shadow-sm shadow-rose-100"
                  }`}>
                    {r.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
