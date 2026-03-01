const https = require('https');

// REPLACE 'YOUR_API_KEY_HERE' with the key obtained at https://aistudio.google.com
const API_KEY = 'YOUR_API_KEY_HERE'; 

async function consultAI(ms, route) {
    const prompt = `Analyze this network metric: Latency of ${ms}ms on route ${route}. 
                    Give me a short terminal-style (8-bit) diagnosis on whether it's stable or if there's congestion.`;

    const data = JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }]
    });

    const options = {
        hostname: 'generativelanguage.googleapis.com',
        path: `/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    };

    return new Promise((resolve) => {
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(body);
                    resolve(json.candidates[0].content.parts[0].text);
                } catch (e) { resolve("ERROR_IA: Could not process the diagnosis."); }
            });
        });
        req.write(data);
        req.end();
    });
}

module.exports = { consultAI };
