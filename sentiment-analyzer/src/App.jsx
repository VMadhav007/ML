import { useState } from "react";
import axios from "axios";
import { Loader2 } from "lucide-react";

function App() {
    const [url, setUrl] = useState("");
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const analyzeVideo = async () => {
        setLoading(true);
        setError("");
        setData(null);

        try {
            const response = await axios.post("http://127.0.0.1:8000/analyze", { url });
            setData(response.data);
        } catch (err) {
            setError("Error analyzing the video. Please check the URL.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 p-6">
            {/* Title */}
            <h1 className="text-3xl font-extrabold text-gray-800 dark:text-white mb-6">
                YouTube Sentiment Analyzer 🎯
            </h1>

            {/* Input & Button */}
            <div className="flex items-center space-x-2">
                <input
                    type="text"
                    placeholder="Enter YouTube Video URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="p-3 border rounded-lg w-96 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                />
                <button
                    onClick={analyzeVideo}
                    className="px-5 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition active:scale-95"
                >
                    Analyze
                </button>
            </div>

            {/* Loading State */}
            {loading && (
                <div className="flex items-center mt-6">
                    <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
                    <p className="ml-2 text-gray-700 dark:text-gray-300">Analyzing...</p>
                </div>
            )}

            {/* Error Message */}
            {error && <p className="mt-4 text-red-500 font-medium">{error}</p>}

            {/* Results */}
            {data && (
                <div className="mt-8 p-6 bg-white dark:bg-gray-800 shadow-lg rounded-lg w-full max-w-2xl">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                        Liking Rate: 
                        <span className="text-green-500 ml-2">{data.liking_rate.toFixed(2)}%</span>
                    </h2>

                    <h3 className="text-lg font-medium mt-4 text-gray-700 dark:text-gray-300">
                        Comments:
                    </h3>
                    <div className="mt-3 space-y-3 max-h-80 overflow-y-auto">
                        {data.comments.map((c, idx) => (
                            <div
                                key={idx}
                                className="p-3 border rounded-lg bg-gray-100 dark:bg-gray-700"
                            >
                                <strong
                                    className={c.sentiment === "Positive" ? "text-green-600" : "text-red-500"}
                                >
                                    {c.sentiment}
                                </strong>
                                <p className="text-gray-800 dark:text-gray-300">{c.comment}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
