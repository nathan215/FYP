import React from "react";

interface CoordinateInputProps {
  label: string;
  value: number;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const CoordinateInput: React.FC<CoordinateInputProps> = ({
  label,
  value,
  onChange,
}) => {
  return (
    <div>
      <label htmlFor={`${label}Input`}>{label}:</label>
      <input
        type="number"
        step="any"
        id={`${label}Input`}
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default CoordinateInput;
