export default function TaskTable({ tasks }: any) {
  return (
    <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6">
      <h2 className="text-xl font-semibold mb-4">Recent Tasks</h2>

      <div className="overflow-auto">
        <table className="w-full text-sm">
          <thead className="text-slate-400 border-b border-slate-800">
            <tr>
              <th className="text-left py-3">ID</th>
              <th className="text-left py-3">Task</th>
              <th className="text-left py-3">Status</th>
              <th className="text-left py-3">Created</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((t: any) => (
              <tr key={t.id} className="border-b border-slate-800/60">
                <td className="py-3">#{t.id}</td>
                <td className="py-3">{t.task}</td>
                <td className="py-3">
                  <span className="rounded-full bg-green-500/10 text-green-400 px-3 py-1">
                    {t.status}
                  </span>
                </td>
                <td className="py-3 text-slate-500">{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
