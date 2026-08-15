package org.ayokoding.enterprise;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity
public class Item {
    @Id @GeneratedValue private Long id;
    private String name;

    protected Item() {}
    Item(String name) { this.name = name; }
    public Long id() { return id; }
    public String name() { return name; }
}

