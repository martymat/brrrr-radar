import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState("loading...");

  useEffect(() => {
    fetch("http://localhost:5000/health")
      .then((res) => res.json())
      .then((data) => {
        setStatus("data.status");
      })
      .catch(() => {
        setStatus("error");
      });
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold">BRRRR Radar</h1>

      <div className="mt-6 rounded border p-4">
        <p className="text-gray-600">
          Backend status:
          <span className="ml-2 font-semibold">{status}</span>
        </p>
      </div>
    </div>
  );
}