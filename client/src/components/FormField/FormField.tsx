import {
  PasswordInputProps,
  __InputProps,
  PasswordInput,
  TextInput,
  Text,
} from '@mantine/core';
import { ReactNode } from 'react';

export interface FormFieldPropsA extends PasswordInputProps, __InputProps {
  inputProps: any;
  withAsterisk?: boolean;
  type?: 'text' | 'password';
  errors?: string | string[] | null | ReactNode;
}

const FormField = ({
  label,
  placeholder,
  type = 'text',
  inputProps,
  errors,
  ...rest
}: FormFieldPropsA) => {
  const InputComponent = type === 'password' ? PasswordInput : TextInput;
  console.log('form field', errors);
  return (
    <div>
      <InputComponent
        label={label}
        placeholder={placeholder}
        {...inputProps}
        error={errors ? true : false}
        {...rest}
      />

      {errors && (
        <div>
          {(Array.isArray(errors) ? errors : [errors]).map((error, index) => (
            <Text key={index} c="red" size="sm">
              {error}
            </Text>
          ))}
        </div>
      )}
    </div>
  );
};

export default FormField;
