import { observer } from 'mobx-react';
import authStore from '../../stores/authStore';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Center, Paper, Stack, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { isEmail, isNotEmpty, useForm } from '@mantine/form';
import FormField from '../../components/FormField/FormField';

const Auth = observer(() => {
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
      email: isEmail('Type your email'),
      password: isNotEmpty('Type your password'),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    await authStore.login(values.email, values.password);
    navigate('/profile');
  });

  return (
    <Center style={{ height: '100vh' }}>
      <Paper withBorder p="xl" radius="md" maw={350}>
        <form onSubmit={handleSubmit}>
          <Stack>
            <FormField
              size="md"
              label="Email"
              placeholder="your@email.com"
              key={form.key('email')}
              inputProps={form.getInputProps('email')}
              errors={form.errors.email}
            />
            <FormField
              size="md"
              type="password"
              label="Password"
              placeholder={visible ? 'qwerty1' : '********'}
              visible={visible}
              maxLength={32}
              onVisibilityChange={toggle}
              min="8"
              key={form.key('password')}
              inputProps={form.getInputProps('password')}
              errors={form.errors.password}
            />
            <Button
              type="submit"
              variant="filled"
              size="md"
              loaderProps={{ type: 'dots' }}
              color="green"
              loading={authStore.status === 'loading' ? true : false}
            >
              Login
            </Button>
            {authStore.status === 'failed' && <p>Error: {authStore.error}</p>}
            <Text size="md">
              Do you not have an account?{' '}
              <Link to="/register">
                <Text span td="underline" c="green">
                  Register
                </Text>
              </Link>
            </Text>
          </Stack>
        </form>
      </Paper>
    </Center>
  );
});

export default Auth;
