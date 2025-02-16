import { observer } from 'mobx-react';
import authStore from '../../stores/authStore';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Center, Paper, Stack, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { isEmail, matchesField, useForm } from '@mantine/form';
import FormField from '../../components/FormField/FormField';

const Register = observer(() => {
  const [visible, { toggle }] = useDisclosure(false);
  const navigate = useNavigate();

  const form = useForm({
    mode: 'uncontrolled',
    validateInputOnChange: true,
    initialValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validate: {
      username: (value) => {
        const errors: string[] = [];
        if (value.length < 5) errors.push('Minimum 5 characters');
        if (value.length > 32) errors.push('Maximum 32 characters');
        if (!/^[a-zA-Z0-9-]+$/.test(value)) {
          errors.push('Only Latin letters, numbers and hyphens are allowed');
        }
        if (/^-|-$/.test(value)) {
          errors.push('The name cannot begin or end with a hyphen.');
        }
        if (/--/.test(value)) {
          errors.push('The name cannot contain two hyphens in a row.');
        }
        return errors.length > 0 ? errors : null;
      },
      email: isEmail('Email is invalid or already taken'),
      password: (value) => {
        const errors: string[] = [];
        if (value.length < 8) errors.push('Minimum 8 characters');
        if (!/[a-zA-Z]/.test(value))
          errors.push('There must be at least one letter');
        if (!/[0-9]/.test(value))
          errors.push('There must be at least one digit');
        if (!/[!@#$%^&*()_+\-=]/.test(value))
          errors.push(
            'There must be at least one special character (!@#$%^&*)',
          );
        if (/\s/.test(value)) errors.push('There should be no spaces');

        return errors.length > 0 ? errors : null;
      },
      confirmPassword: matchesField('password', 'Passwords are not the same'),
    },
  });

  const handleSubmit = form.onSubmit(
    async (values) => {
      await authStore.register(values.email, values.username, values.password);
      console.log(`
        username: ${values.username},
        pass: ${values.password},
        email: ${values.email},
        `);
      navigate('/profile');
    },
    (errors) => {
      const firstErrorPath = Object.keys(errors)[0];
      form.getInputNode(firstErrorPath)?.focus();
      console.log(form.errors);
    },
  );

  return (
    <Center style={{ height: '100vh' }}>
      <Paper withBorder p="xl" radius="md" maw={350}>
        <form onSubmit={handleSubmit}>
          <Stack>
            <FormField
              label="Username"
              inputProps={form.getInputProps('username')}
              errors={form.errors.username}
              placeholder="username"
              maxLength={32}
              withAsterisk
              size="md"
              key={form.key('username')}
              description="Username should be at least 5 characters, only latin letters, numbers and hyphens are allowed"
            />
            <FormField
              label="Email"
              inputProps={form.getInputProps('email')}
              errors={form.errors.email}
              placeholder="your@email.com"
              maxLength={32}
              withAsterisk
              size="md"
              key={form.key('email')}
            />
            <FormField
              label="Password"
              type="password"
              inputProps={form.getInputProps('password')}
              errors={form.errors.password}
              placeholder={visible ? 'qwerty1' : '********'}
              visible={visible}
              maxLength={32}
              onVisibilityChange={toggle}
              withAsterisk
              size="md"
              key={form.key('password')}
              description="Password should be at least 8 characters, at least one letter, one digit and one special character"
            />
            <FormField
              label="Confirm password"
              type="password"
              inputProps={form.getInputProps('confirmPassword')}
              errors={form.errors.confirmPassword}
              placeholder={visible ? 'qwerty1' : '********'}
              visible={visible}
              maxLength={32}
              onVisibilityChange={toggle}
              withAsterisk
              size="md"
              key={form.key('confirmPassword')}
            />
            <Button
              type="submit"
              variant="filled"
              size="md"
              loaderProps={{ type: 'dots' }}
              color="green"
              loading={authStore.status === 'loading' ? true : false}
            >
              Register
            </Button>
            <Text size="md">
              Do you have an account?{' '}
              <Link to="/login">
                <Text span td="underline" c="green">
                  Login
                </Text>
              </Link>
            </Text>
            {authStore.status === 'failed' && <p>Error: {authStore.error}</p>}
          </Stack>
        </form>
      </Paper>
    </Center>
  );
});

export default Register;
