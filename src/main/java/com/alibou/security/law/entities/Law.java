package com.alibou.security.law.entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class Law {
    @Id
    private UUID id;
    private String name;
    private String nameRu;
    private String nameEn;
    @Enumerated(EnumType.STRING)
    private LawType lawType;
    private String link;

    @Lob
    private byte[] bytes;
    private String fileType;
    private String fileName;
}
