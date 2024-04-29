import React from "react";

const FormInput = (props) => {
  const { id, onChange, ...inputProps } = props;
  return (
    <div>
      <label>
        <input {...inputProps} className="p-2 rounded-md text-black w-full" />
      </label>
    </div>
  );
};

export default FormInput;
