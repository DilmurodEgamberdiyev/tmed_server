package com.alibou.security.about.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class About {
    @Id
    private UUID id;
    @Column(columnDefinition = "text", length = 8192)
    private String description;
    private String descriptionRu;
    private String descriptionEn;
}
