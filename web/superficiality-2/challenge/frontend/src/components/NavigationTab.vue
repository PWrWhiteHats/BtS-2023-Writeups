<script>

import { RouterLink } from 'vue-router'

export default {
  props: ['toLink', 'icon', 'isActive']
}

</script>

<template>
  <li class="nav-item">
    <RouterLink
      class="nav-link"
      :class="{'active': isActive}"
      :to="toLink"
    >
      <div
        class="border-bottom border-2 p-2"
        :class="{'border-danger': isActive}"
      >
        <i class="bi" :class="icon"></i>
      </div>
    </RouterLink>
  </li>
</template>
