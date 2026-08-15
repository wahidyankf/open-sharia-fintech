package org.ayokoding.enterprise;

import org.springframework.data.jpa.repository.JpaRepository;

interface ItemRepository extends JpaRepository<Item, Long> {}
