// components/common/Button.jsx
export default function Button({
  icon,
  label,
  onClick,
  disabled = false,
  fullWidth = false,
  variant = "primary",
}) {
  const baseClasses =
    "flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors";
  const variantClasses = {
    primary: "bg-blue-500 text-white hover:bg-blue-600 disabled:bg-blue-300",
    outline:
      "border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:text-gray-400",
  };
  const widthClass = fullWidth ? "w-full" : "";

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${widthClass}`}
      onClick={onClick}
      disabled={disabled}
    >
      {icon && <span className="mr-2">{icon}</span>}
      {label}
    </button>
  );
}
