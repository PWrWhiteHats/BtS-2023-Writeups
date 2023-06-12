<script>

export default {
  props: ['title', 'isActive', 'toTab'],
}
</script>

<template>
  <div
    class="nav-item me-3 border-bottom border-3"
    :class="{'border-danger-subtle': isActive}"
  >
    <RouterLink
      class="nav-link link-light text-start"
      :class="{'active': isActive}"
      :to="{name: toTab}"
    >{{ title }}</RouterLink>
  </div>
</template>

<style scoped>
  .nav-item {
    cursor: pointer;
  }

  .nav-link {
    &:hover {
      color: var(--bs-secondary-color);
    }
  }

  .nav-link.active {
    &:hover {
      color: initial;
    }
  }

  a {
    color: white;
  }
</style>
