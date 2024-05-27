package com.alibou.security.law.entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class Law {
    @Id
    private UUID id;
    private String name;
    private String nameRu;
    private String nameEn;
    @Enumerated(value = EnumType.STRING)
    private LawType lawType;
    @Column(columnDefinition = "text", length = 8192)
    private String link;

    @Lob
    private byte[] bytes;
    private String fileType;
    private String fileName;
}
