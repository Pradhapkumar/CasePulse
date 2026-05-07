const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Simple in-memory cache: "text|lang" => "translated"
const cache = new Map();

/**
 * Translate text to target language.
 * Falls back gracefully to original text on error.
 */
export const translateText = async (text, targetLanguage) => {
  if (!text || targetLanguage === "en") return text;

  const cacheKey = `${text}|${targetLanguage}`;
  if (cache.has(cacheKey)) return cache.get(cacheKey);

  try {
    const res = await fetch(`${API_BASE_URL}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, target_language: targetLanguage }),
    });

    if (!res.ok) throw new Error(`Translate API error: ${res.status}`);
    const data = await res.json();
    const translated = data.translated_text ?? text;
    cache.set(cacheKey, translated);
    return translated;
  } catch (err) {
    console.error("[translateService] Translation failed:", err);
    return text;
  }
};

/**
 * Translate multiple strings. Returns same-keyed object with translated values.
 */
export const translateMany = async (textMap, targetLanguage) => {
  if (targetLanguage === "en") return textMap;
  const entries = Object.entries(textMap);
  const translated = await Promise.all(
    entries.map(([key, val]) =>
      translateText(val, targetLanguage).then((r) => [key, r])
    )
  );
  return Object.fromEntries(translated);
};
