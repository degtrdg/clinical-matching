interface DataObject {
  [key: string]: number;
}

interface HorizontalBarGraphProps {
  data: DataObject;
  selected: string;
  onChange: (key: string) => void;
}

const HorizontalBarGraph: React.FC<HorizontalBarGraphProps> = ({ data, selected, onChange }) => {
  const maxValue = Math.max(...Object.values(data));
  const totalValue = Object.values(data).reduce((a, b) => a + b, 0);

  return (
    <div className="space-y-4">
      {Object.entries(data).map(([label, value]) => {
        const percentage = ((value / totalValue) * 100).toFixed(2);
        const barWidth = Math.max((value / maxValue) * 100, 1); // Ensure a minimum bar width for visibility

        return (
          <div key={label} className="flex items-center">
            <input
              type="radio"
              id={label}
              name="dataSelection"
              value={label}
              checked={selected === label}
              onChange={() => onChange(label)}
              className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500 mr-2"
            />
            <label htmlFor={label} className="flex items-center mr-2">
              <span className="text-sm font-medium text-gray-900">{label}</span>
            </label>
            <div className="flex-1 bg-gray-200 rounded h-6 overflow-hidden">
              <div
                className={`bg-indigo-600 h-6 rounded ${percentage === '0.00' ? 'w-0' : ''}`}
                style={{ width: `${barWidth}%` }}
              ></div>
            </div>
            <span className="text-sm font-medium text-gray-900 mr-2 pl-2">{percentage}%</span>
          </div>
        );
      })}
    </div>
  );
};

export default HorizontalBarGraph;
