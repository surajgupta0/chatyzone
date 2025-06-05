// components/Layout/Panel.jsx
export default function Panel({ position, width, children }) {
  const positionClasses = {
    left: "border-r border-gray-200",
    center: "flex flex-col",
    right: "border-l border-gray-200",
  };

  return (
    <div
      className={`${width} ${positionClasses[position]} h-full overflow-hidden`}
    >
      {children}
    </div>
  );
}
