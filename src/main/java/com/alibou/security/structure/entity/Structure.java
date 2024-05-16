package com.alibou.security.structure.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class Structure {
    @Id
    private UUID id;

    @Lob
    private byte[] bytes;
    private String fileType;
    private String fileName;
}
