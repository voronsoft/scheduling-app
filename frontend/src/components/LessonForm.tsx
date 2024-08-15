import { useAdminStore } from "../store/store";
import { observer } from 'mobx-react-lite';

const LessonForm = observer(() => {
  const store = useAdminStore();

  return (
    <div>New Better LessonForm</div>
  )
})

export default LessonForm;