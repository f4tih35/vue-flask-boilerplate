<template>
  <div class="todo-container">
    <h2>To-Do List</h2>
    <ul class="todo-list">
      <transition-group name="bounce" tag="div">
        <li v-for="todo in todos" :key="todo.id" :class="{ done: todo.done }">
          <div class="todo-item">
             <div @click="toggleDone(todo)">
              {{ todo.title }}
            </div>
            <div>
              <button @click="editTodo(todo)">Edit</button>
              <button @click="deleteTodo(todo.id)">Delete</button>
            </div>
          </div>
        </li>
      </transition-group>
    </ul>
    <div class="todo-form">
      <input v-model="editingTodo.title" @keyup.enter="saveTodo" placeholder="Add a new todo">
      <button @click="saveTodo">Save</button>
      <button v-if="editingTodo.id" @click="cancelEdit">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      todos: [],
      editingTodo: {},
    };
  },
  created() {
    this.fetchTodos();
  },
  methods: {
    fetchTodos() {
      axios.get("/todos").then(response => {
        this.todos = response.data.todos;
      });
    },
    addTodo() {
      axios.post("/todos", this.editingTodo).then(() => {
        this.editingTodo = {};
        this.fetchTodos();
      });
    },
    deleteTodo(id) {
      axios.delete(`/todos/${id}`).then(() => {
        this.fetchTodos();
      });
    },
    editTodo(todo) {
      this.editingTodo = { ...todo };
    },
    saveTodo() {
      if (this.editingTodo.id) {
        axios.put(`/todos/${this.editingTodo.id}`, this.editingTodo).then(() => {
          this.editingTodo = {};
          this.fetchTodos();
        });
      } else {
        this.addTodo();
      }
    },
    cancelEdit() {
      this.editingTodo = {};
    },
    toggleDone(todo) {
      axios.put(`/todos/${todo.id}/toggle`).then(response => {
        todo.done = response.data.todo.done;
      });
    },
  },
};
</script>

<style scoped>
.todo-container {
  max-width: 400px;
  margin: auto;
}

.todo-list {
  margin: 0;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  border-radius: 4px;
}

.done .todo-item {
  background-color: #f8f9fa;
  text-decoration: line-through;
}

.todo-form input {
  margin-right: 10px;
}
</style>
