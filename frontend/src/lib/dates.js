// Tiny date helpers
export function formatRelativeGroup(date) {
  if (!(date instanceof Date)) date = new Date(date);
  const now = new Date();
  const diff = (now - date) / (1000 * 60 * 60 * 24);
  if (diff < 1) return "Today";
  if (diff < 2) return "Yesterday";
  if (diff < 7) return "Last 7 days";
  return "Earlier";
}
