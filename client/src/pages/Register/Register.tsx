import { useState } from 'react';

const Register = () => {
  const [login, setLogin] = useState();
  const [password, setPassword] = useState();

  return (
    <div>
      <form>
        <div>
          <label htmlFor="">Логин</label>
          <input type="text" />
        </div>
        <div>
          <label htmlFor="">Пароль</label>
          <input type="text" />
        </div>
      </form>
    </div>
  );
};

export default Register;
